# 反反爬经验库

> 团队共同维护，遇到新的反爬手段请在此补充。

## 通用策略

### 请求频率控制

- 使用 `packages/anti_detect/rate_limiter.py` 控制频率
- 默认 1 req/s，不要贪快
- 加随机延迟：`time.sleep(random.uniform(0.5, 1.5))`

### User-Agent 轮换

- 使用 `packages/http/fingerprint.py` 的 `get_random_ua()`
- HttpClient 已内置 UA 轮换

### 代理轮换

- 使用 `packages/http/proxy_pool.py`
- 代理挂了自动剔除，定期刷新

### Cookie 管理

- 使用 `packages/anti_detect/cookie_manager.py`
- Cookie 有有效期，过期自动刷新

## 常见反爬类型

### 1. IP 封禁

**特征**：HTTP 403/429，或返回验证码页面

**应对**：
- 降低频率
- 切换代理
- 加随机延迟

### 2. 验证码

**特征**：跳转到验证码页面

**应对**：
- 接入打码平台（在 `packages/anti_detect/captcha.py` 中扩展）
- 降频避免触发

### 3. JavaScript 渲染

**特征**：requests 拿到的页面是空的或加载中

**应对**：
- 用 Playwright / Selenium
- 找接口直接调 API（优先）

### 4. 请求签名

**特征**：请求参数中有 sign/token/timestamp

**应对**：
- 抓包分析签名算法
- 用 Node.js 执行签名 JS
- 记录到本文档供团队参考

### 5. 登录态检测

**特征**：未登录返回不同内容

**应对**：
- Cookie 登录态管理
- 定期刷新 Token

## 站点经验（按字母排序）

> 每攻克一个站，在此记录要点

<!-- 示例格式：
### GitHub
- 无需代理
- 注意 rate limit（未认证 60 req/h，认证 5000 req/h）
- Trending 页面直接解析 HTML，无需 JS 渲染
-->
