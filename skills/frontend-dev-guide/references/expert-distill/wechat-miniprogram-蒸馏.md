# 微信小程序开发专家蒸馏 · WeChat Mini Program Developer（小程达）

> **来源**：WorkBuddy 专家中心「小程达·微信小程序开发」专家包蒸馏（2026-09-06）
> **源包**：`~/.workbuddy/plugins/marketplaces/experts/plugins/we-chat-mini-program-developer/agents/we-chat-mini-program-developer.md`（360 行）
> **蒸馏方式**：并入 frontend-dev-guide 的 expert-distill（前端延伸岗：小程序）。
> **去重说明**：组件/状态管理/通用前端方法论不重复；本文档**只保留微信生态特有增量**——平台硬约束、setData 性能纪律、登录/支付/订阅消息集成模式、过审要点、量化指标与内容安全。代码模板属落地示例，提取规则与模式。

---

## 一、平台硬约束（设计前先背下）

1. **域名白名单**：所有 API/WebSocket/上传/下载域名必须先在微信后台注册——未注册直接失败
2. **HTTPS 强制**：每个请求必须 HTTPS + 有效证书
3. **包体纪律**：主包 <2MB（目标 <1.5MB），总包 20MB 含分包；大功能用分包（`subpackages/`）按用户旅程优先级拆分
4. **隐私合规**：敏感 API 先授权再访问；无页面可见用途的权限申请会被拒审（如页面没用到定位却申请位置权限）
5. **无 DOM**：双线程架构，直接 DOM 操作不可能——一切走数据绑定（setData）

---

## 二、setData 性能纪律（性能头号关键）

> 每次 setData 都跨 JS-native 桥——高频大 payload 是卡顿主因。

1. **只传视图需要的字段**：接口返回 30 字段，页面只用 8 个 → setData 只发这 8 个（别整包塞）
2. **合并多次 setData 为一次**：一次回调里攒齐再 setData
3. **延迟非关键数据**：首屏先渲染核心（如图片先 slice(0,5)），其余 setTimeout 500ms 后再补
4. **纯数据字段**（pureDataPattern）：非视图用数据不进 data
5. **虚拟列表**：长列表用 recycle-view（组件库）而非整渲
6. 图片 CDN + WebP + 懒加载 + 尺寸裁剪

---

## 三、核心集成模式（登录/支付/订阅）

### 登录流程（wx.login → code → 服务端换 session → 存 token）
```
wx.login() 取 code → 发服务端 /auth/wechat-login → 后端 code2session 换 openid/session_key
→ 服务端签发 access_token + refresh_token → 前端存 storage
→ 请求 401 → refreshTokenAndRetry（静默续期重试）
```

### 微信支付（两步：服务端建单拿参 → 前端 wx.requestPayment）
- 服务端：创建订单 → 调微信统一下单 → 返回 timeStamp/nonceStr/package(prepay_id)/signType/paySign
- 前端：`wx.requestPayment(...)` → success 记 orderId；**fail 区分 `cancel`（用户取消，正常）与真失败**
- 服务端必须：验签 + 回调验签 + 退款流程（防伪造支付回调）

### 订阅消息（替代已废弃的模板消息）
- **最佳请求时机**：用户刚完成关键动作后立刻请求授权（如下单后——此时转化最高），不要冷启动就要
- `wx.requestSubscribeMessage({ tmplIds })` → 过滤 res[id] === 'accept'

---

## 四、社交分发（小程序增长内建）

- `onShareAppMessage`（好友/群）+ `onShareTimeline`（朋友圈）：title/path/imageUrl 必配
- 分享带参数（`?id=xxx`）回跳落地页
- 目标：分享→打开转化率 >15%

---

## 五、过审要点（一次通过 90%+）

- 隐私政策 + 授权流程完整、内容合规
- **权限申请有页面可见用途**（页面上真有这个场景）
- UGC 内容用安全接口：`msgSecCheck`（文本）+ `imgSecCheck`（图片）
- 多端真机测试（iOS/Android 微信、多机型/网络/基础库版本）
- DevTools 提交前自测：真机预览 + 性能审计（目标 >90/100）

---

## 六、量化成功指标（验收基线）

| 指标 | 目标 |
|------|------|
| 启动时间 | <1.5s（中端 Android） |
| 主包大小 | <1.5MB（分包策略） |
| 审核 | 一次通过率 ≥90% |
| 崩溃率 | <0.1%（全基础库版本） |
| 分享→打开转化 | >15% |
| 7 日留存 | >25%（核心用户群） |
| DevTools 性能分 | >90/100 |

---

## 七、生态联动（流量来源）

公众号双向导流（文章→小程序）、视频号嵌入小程序链接（短视频/直播带货）、企业微信（内部工具/客户沟通）、小商店/直播（电商场景）。跨多端用 Taro/uni-app（一套代码微信/支付宝/百度/字节），需要适配层处理 API 差异。

---

## 八、与 frontend-dev-guide 已有蒸馏的配合

| 文档 | 定位 |
|------|------|
| mvp-frontend-蒸馏 / frontend-developer-蒸馏 | Web 端工艺与性能 |
| mobile-developer-蒸馏（掌中灵） | iOS/Android App |
| **wechat-miniprogram-蒸馏（本文档）** | **微信小程序（含 Taro/uni-app 跨端）：平台约束 / setData 纪律 / 支付订阅登录 / 过审 / 量化指标** |

> **使用原则**：项目含微信小程序端时读本文档——包体与域名约束先行、setData 纪律贯穿、支付/订阅按模式接、提交前过审 checklist。Taro 跨端项目同步参考 mvp-frontend 的 CSS 工艺。

---

_蒸馏记录：v1.0（2026-09-06）· 专家「小程达」→ frontend-dev-guide/expert-distill/_
