# Gmail OAuth 设置指南

## 概述

本应用使用 Gmail API 来搜索工作相关邮件、发送定制简历和求职信。要使用这些功能，您需要设置 Google OAuth 2.0 认证。

## 设置步骤

### 1. 创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 记录项目 ID

### 2. 启用 Gmail API

1. 在 Google Cloud Console 中，转到 "APIs & Services" > "Library"
2. 搜索 "Gmail API"
3. 点击 "Enable" 启用 API

### 3. 创建 OAuth 2.0 凭据

1. 转到 "APIs & Services" > "Credentials"
2. 点击 "Create Credentials" > "OAuth 2.0 Client IDs"
3. 选择 "Web application" 作为应用程序类型
4. 设置名称（例如：Job Application Automation）

### 4. 配置已获授权的重定向 URI

**重要提示：您在下面添加的 URI 的网域将自动添加到 OAuth 权限请求页面作为已获授权的网域。**

#### 已获授权的 JavaScript 来源
适用于来自浏览器的请求：
```
http://localhost:3000
https://localhost:3000
http://127.0.0.1:3000
```

#### 已获授权的重定向 URI
适用于来自 Web 服务器的请求：
```
http://localhost:3000/auth/gmail/callback
https://localhost:3000/auth/gmail/callback
http://127.0.0.1:3000/auth/gmail/callback
```

**生产环境 URI（替换为您的域名）：**
```
https://yourdomain.com/auth/gmail/callback
https://www.yourdomain.com/auth/gmail/callback
```

### 5. 获取客户端凭据

1. 创建凭据后，下载 JSON 文件或复制以下信息：
   - Client ID
   - Client Secret

### 6. 配置环境变量

在 `backend/.env` 文件中设置以下变量：

```env
# Gmail API 配置
GMAIL_CLIENT_ID=your-gmail-client-id-here
GMAIL_CLIENT_SECRET=your-gmail-client-secret-here
```

### 7. OAuth 同意屏幕配置

1. 转到 "APIs & Services" > "OAuth consent screen"
2. 选择 "External" 用户类型（用于测试）
3. 填写必要信息：
   - App name: Job Application Automation
   - User support email: 您的邮箱
   - Developer contact information: 您的邮箱

4. 添加作用域：
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.modify`

5. 添加测试用户（在发布前）：
   - 添加您要测试的 Gmail 账户

## 重要注意事项

### 设置生效时间
**注意：设置可能需要 5 分钟到几小时才会生效**

### 测试环境 vs 生产环境

#### 测试环境
- 使用 `http://localhost:3000` 作为重定向 URI
- 应用状态设置为 "Testing"
- 只有添加的测试用户可以使用

#### 生产环境
- 使用 HTTPS 重定向 URI
- 应用需要通过 Google 验证
- 所有用户都可以使用

### 安全最佳实践

1. **永远不要在代码中硬编码客户端密钥**
2. **使用环境变量存储敏感信息**
3. **定期轮换客户端密钥**
4. **监控 API 使用情况**

## 使用流程

### 1. 获取授权 URL
```bash
GET /api/v1/auth/gmail/auth-url
Authorization: Bearer <your-jwt-token>
```

### 2. 用户授权
用户访问返回的 `auth_url`，登录 Google 账户并授权应用

### 3. 处理回调
用户授权后，Google 会重定向到您的回调 URL，包含授权码

### 4. 交换令牌
```bash
POST /api/v1/auth/gmail/authorize
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "authorization_code": "received-authorization-code"
}
```

### 5. 检查连接状态
```bash
GET /api/v1/auth/gmail/status
Authorization: Bearer <your-jwt-token>
```

## 故障排除

### 常见错误

1. **redirect_uri_mismatch**
   - 确保重定向 URI 完全匹配（包括协议、域名、端口、路径）
   - 检查是否有多余的斜杠

2. **invalid_client**
   - 检查客户端 ID 和密钥是否正确
   - 确保 API 已启用

3. **access_denied**
   - 用户拒绝了授权
   - 检查请求的作用域是否过多

4. **invalid_grant**
   - 授权码已过期或已使用
   - 重新获取授权码

### 调试技巧

1. 检查 Google Cloud Console 中的 API 使用情况
2. 查看应用日志中的详细错误信息
3. 使用 Google OAuth 2.0 Playground 测试作用域
4. 确认时间同步（JWT 令牌对时间敏感）

## API 限制

- Gmail API 有每日配额限制
- 建议实现适当的缓存和重试机制
- 监控 API 使用情况以避免超出限制

## 支持

如果遇到问题，请检查：
1. Google Cloud Console 中的错误日志
2. 应用程序日志
3. [Gmail API 文档](https://developers.google.com/gmail/api)
4. [OAuth 2.0 文档](https://developers.google.com/identity/protocols/oauth2)