import os
import time
import io
from playwright.sync_api import sync_playwright
from PIL import Image
import imageio

def capture_fullpage_gif(url: str, output_gif_path: str, duration: int = 3, capture_fps: int = 10):
    frames = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()

        print(f"Loading {url} ...")
        page.goto(url, timeout=60000)

        # 전체 페이지 크기 (최대 1024x720 제한)
        dimensions = page.evaluate("""() => {
            return {
                width: document.documentElement.scrollWidth,
                height: document.documentElement.scrollHeight
            };
        }""")

        width = min(dimensions["width"], 1024)
        height = min(dimensions["height"], 720)

        # 짝수 픽셀 맞춤
        width -= width % 2
        height -= height % 2

        page.set_viewport_size({"width": width, "height": height})

        print(f"Viewport set to: {width}x{height}")

        # 폰트 로딩 완료 대기
        print("Waiting for fonts to load...")
        page.evaluate_handle("document.fonts.ready.then(() => {})")

        total_frames = duration * capture_fps
        frame_interval = 1 / capture_fps

        # 프레임 반복 캡처
        for frame_num in range(total_frames):
            print(f"Capturing frame {frame_num + 1}/{total_frames}")
            try:
                screenshot_bytes = page.screenshot(type="png", timeout=60000)
                image = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")

                # 메모리 최적화를 위해 해상도 절반 축소
                image = image.resize((image.width // 2, image.height // 2))

                frames.append(image)
            except Exception as e:
                print(f"Frame {frame_num + 1}: Failed to capture - {e}")
                continue  # 실패해도 다음 프레임으로 넘어감

            time.sleep(frame_interval)

        browser.close()

    if not frames:
        raise RuntimeError("No frames captured. Cannot save GIF.")

    # GIF로 저장 (loop, 최적화)
    print(f"Saving to {output_gif_path} ...")
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / capture_fps),
        loop=0,
        optimize=True
    )
    print(f"GIF saved to {output_gif_path}")
