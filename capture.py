from playwright.sync_api import sync_playwright
from PIL import Image
import imageio
import io
import time

def capture_fullpage_webp(url: str, output_webp_path: str, duration: int = 5, capture_fps: int = 15, playback_fps: int = 5, quality: int = 85, method: int = 6):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print(f"Loading {url} ...")
        page.goto(url, timeout=60000)

        # Lazy load 스크롤
        scroll_height = page.evaluate("() => document.body.scrollHeight")
        viewport_height = page.viewport_size["height"]
        for i in range(0, scroll_height, viewport_height//2):
            page.evaluate(f"window.scrollTo(0, {i})")
            time.sleep(0.2)
        page.evaluate("window.scrollTo(0, 0)")

        # 전체 페이지 크기 설정
        dimensions = page.evaluate("""() => {
            return {
                width: document.documentElement.scrollWidth,
                height: document.documentElement.scrollHeight
            };
        }""")
        page.set_viewport_size({"width": dimensions["width"], "height": dimensions["height"]})

        total_frames = duration * capture_fps
        frame_interval = 1 / capture_fps

        frames = []

        print(f"Capturing {total_frames} frames for WebP...")

        for _ in range(total_frames):
            screenshot_bytes = page.screenshot(type="png")
            image = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")
            frames.append(image)
            time.sleep(frame_interval)

        # 저장할 때 playback_fps 로 재생 속도 조정
        print(f"Saving Animated WebP to {output_webp_path} ...")
        imageio.mimsave(
            output_webp_path,
            frames,
            format="WEBP",
            fps=playback_fps,
            loop=0,
            quality=quality,
            method=method
        )

        print(f"WebP saved to {output_webp_path}")
        browser.close()