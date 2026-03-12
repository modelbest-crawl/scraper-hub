"""
冒烟测试：真实发请求，验证目标站点状态
标记为 smoke，默认不运行，需手动 make test-smoke 触发
"""

import pytest


@pytest.mark.smoke
def test_target_accessible():
    """验证目标站点还能访问"""
    # TODO: 替换为实际目标 URL
    # import requests
    # resp = requests.get("https://target-site.com", timeout=10)
    # assert resp.status_code == 200
    pass
