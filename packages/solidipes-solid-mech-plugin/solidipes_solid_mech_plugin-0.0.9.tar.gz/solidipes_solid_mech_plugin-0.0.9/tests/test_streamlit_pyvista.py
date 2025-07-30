import os
import shutil
import signal
import subprocess
import time

import pytest
import utils

streamlit_port = 8504
max_connection_tries = 20
delay_connection_trial = 1
max_loading_checks = 20
delay_page_load = 1
test_download_dir = os.path.join(os.getcwd(), "_downloads")


@pytest.fixture()
def sb(request):
    from selenium import webdriver
    from seleniumbase import BaseCase

    class BaseClass(BaseCase):
        def get_new_driver(self, *args, **kwargs):
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            self.download_dir = test_download_dir
            os.makedirs(self.download_dir, exist_ok=True)
            firefox_profile = {
                "browser.download.folderList": 2,
                "browser.download.dir": self.download_dir,
                "browser.helperApps.neverAsk.saveToDisk": "image/png",
                "pdfjs.disabled": True,
            }
            for key, value in firefox_profile.items():
                options.set_preference(key, value)
            return webdriver.Firefox(options=options)

        def setUp(self):
            super().setUp()

        def base_method(self):
            pass

        def tearDown(self):
            self.save_teardown_screenshot()
            super().tearDown()

    sb = BaseClass("base_method")
    sb.setUpClass()
    sb.setUp()
    yield sb
    sb.tearDown()
    sb.tearDownClass()


class WebReportLauncher:
    def __init__(self):
        self.streamlit_subprocess = None
        self.out = None
        self.err = None

    def launch(self, dir_path):
        self.streamlit_subprocess = subprocess.Popen(
            [
                "solidipes",
                "report",
                "web-report",
                dir_path,
                "--server.port",
                str(streamlit_port),
                "--server.headless",
                "true",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,
        )
        return self

    def terminate(self):
        if not self.streamlit_subprocess:
            return
        os.killpg(os.getpgid(self.streamlit_subprocess.pid), signal.SIGTERM)
        try:
            self.out, self.err = self.streamlit_subprocess.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            return None, ""
        self.streamlit_subprocess = None

    def get_outputs(self):
        return self.out, self.err


@pytest.fixture()
def web_report():
    web_report_launcher = WebReportLauncher()
    yield web_report_launcher
    web_report_launcher.terminate()


def init_study_dir(tmp_path, solidipes=True, git=False, git_remote=False):
    dir_path = tmp_path / "study"
    if not os.path.exists(f"{tmp_path}/study"):
        dir_path.mkdir()
    if solidipes:
        subprocess.run(["solidipes", "init"], cwd=dir_path)
    if git or git_remote:
        subprocess.run(["git", "init", "-q"], cwd=dir_path)
    if git_remote:
        subprocess.run(
            ["git", "remote", "add", "origin", "https://domain.com/subdomain/user_name/project_name.git"], cwd=dir_path
        )
    return dir_path


def check_streamlit_is_loading(sb):
    return sb.is_element_present('div[data-testid="stStatusWidget"]')


def start_web_report_without_fault(sb, dir_path, web_report, target="?page=curation"):
    web_report.launch(dir_path)
    url = f"http://localhost:{streamlit_port}/{target}"
    for i in range(max_connection_tries):
        try:
            sb.open(url)
            break
        except Exception:
            time.sleep(delay_connection_trial)
    for i in range(max_loading_checks):
        time.sleep(delay_page_load)
        if not check_streamlit_is_loading(sb):
            break
    time.sleep(delay_page_load)


def gracefully_stop_report(web_report):
    web_report.terminate()
    _, streamlit_errors = web_report.get_outputs()
    streamlit_errors = str(streamlit_errors).replace("\\n", "\n")
    error_found = "Traceback" in streamlit_errors or "already in use" in streamlit_errors
    if error_found:
        raise RuntimeError("Error encountered in Streamlit: \n{}".format(streamlit_errors))


def click_solidipes_mesh_button(sb):
    print("Start streamlit-pyvista test")
    sb.click("button:contains('pyvista_mesh.vtu')")
    sb.wait(10)


def click_wireframe_checkbox(sb):
    sb.click("label[for='wireframe_checkbox']")
    print("Clicked on the wireframe checkbox")


def download_mesh(sb):
    download_button = "button.v-btn i.mdi-file-png-box"
    sb.click(download_button)
    sb.wait(10)


def test_streamlit_pyvista_in_web_report(sb, tmp_path, web_report):
    dir_path = init_study_dir(tmp_path, git=True)
    os.makedirs(f"{dir_path}/data", exist_ok=True)
    shutil.copy2(utils.get_asset_path("pyvista_mesh.vtu"), f"{dir_path}/data/")
    start_web_report_without_fault(sb, dir_path, web_report, target="?page=display_page&file=./data/pyvista_mesh.vtu")
    iframes = sb.find_elements('iframe[data-testid="stIFrame"]')
    assert len(iframes) > 0
    sb.switch_to_frame(iframes[0])
    click_wireframe_checkbox(sb)
    download_mesh(sb)
    download_dir = sb.download_dir
    downloaded_files = [f for f in os.listdir(download_dir) if f.endswith(".png")]
    if downloaded_files:
        downloaded_file = downloaded_files[0]
        download_path = os.path.join(download_dir, downloaded_file)
        print(f"Downloaded in {download_path}")
        assert os.path.exists(download_path), f"Downloaded file not found at {download_path}"
        assert utils.image_similarity(download_path, utils.get_asset_path("test_mesh_loaded.png"))
        print("Files matches expected results")
        os.remove(download_path)
    else:
        print("No files were downloaded")
    sb.switch_to_default_content()
    gracefully_stop_report(web_report)
