"""
Examples for Computer Use SDK
"""
from .client import new_computer_use_client


def example_basic_operations():
    """
    Example of basic mouse and keyboard operations
    """
    # Initialize the client
    client = new_computer_use_client("http://localhost:8102")

    # Get screen size
    screen_size_response = client.get_screen_size()
    print(f"Screen size: {screen_size_response}")
    ret = client.move_mouse(100,100)
    print(f"MoveMouse response: {ret}")
    ret = client.click_mouse(100,120,"right")
    print(f"ClickMouse response: {ret}")
    client.type_text("Hello World")
    print(f"TypeText response: {client.type_text('Hello World')}")
    client.press_key("enter")
    print(f"PressKey response: {client.press_key('enter')}")
    client.click_mouse(100,100,"right")
    print(f"ClickMouse response: {client.click_mouse(100,100,"right")}")
    ret = client.get_cursor_position()
    print(f"Cursor position: {ret}")

    # file and command
    ret = client.list_processes()
    print(f"list_processes response: {ret}")
    ret = client.list_sessions()
    print(f"list_sessions response: {ret}")
    ret = client.list_directory("/Users/bytedance")
    print(f"list_directory response: {ret}")
    ret = client.create_file("/Users/bytedance/Downloads/3.txt",b"Hellllllllo World")
    print(f"create_file response: {ret}")
    ret = client.read_file("/Users/bytedance/Downloads/3.txt")
    print(f"read_file response: {ret}")
    ret = client.read_multi_files(["/Users/bytedance/Downloads/2.txt","/Users/bytedance/Downloads/1.txt"])
    print(f"read_multi_files response: {ret}")
    ret = client.search_file("/Users/bytedance/Downloads",".*\.txt")
    print(f"search_file response: {ret}")
    ret = client.execute_command("ls -l")
    print(f"execute_command response: {ret}")

if __name__ == "__main__":
    print("Running basic operations example:")
    example_basic_operations()