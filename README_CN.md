# Neon Harbor 手机应用封装包

这个包保留了你上传的 Neon Harbor 网页游戏，并添加了 PWA 配置与 Capacitor 封装配置。

## 包含内容
- `www/`：网页游戏文件（index.html、Three.js、Socket.IO 客户端）以及 PWA manifest / service worker / 图标。
- `package.json`、`capacitor.config.ts`：用于封装 Android / iOS 的项目配置。
- `.github/workflows/build-android.yml`：上传到 GitHub 后，可通过 Actions 云端构建 Android Debug APK。
- `desktop-original/`：原来的 Python 桌面启动器与日志，仅作备份；手机应用不需要运行 Python 启动器。

## 最简单的零成本路线
1. 把 `www` 文件夹部署到 GitHub Pages 或 Cloudflare Pages。
2. iPhone：用 Safari 打开部署网址 → 分享 → 添加到主屏幕。无需 Apple Developer 付费会员，也不需要签名。这是网页应用，不是 App Store 原生应用。
3. Android：可以同样使用网页版本；若需要独立 APK，使用下面的 Capacitor / GitHub Actions 流程。

## Android APK（云端构建）
1. 把这个文件夹里的所有内容上传到一个新的 GitHub 仓库根目录（包括隐藏的 `.github` 文件夹）。
2. 打开仓库的 Actions 标签页，启用 Actions。
3. 选择 `Build Neon Harbor Android APK`，点击 `Run workflow`。
4. 成功后打开该次运行记录，在 Artifacts 区域下载 `NeonHarbor-Android-debug`。
5. 解压后得到 `app-debug.apk`，可以安装到 Android 手机上。Debug APK 适合测试，不是商店发布版本。

## iOS 原生 App 的限制
- `npx cap add ios` 需要在 macOS 上运行并使用 Xcode 生成/编译 iOS 工程。
- 没有付费 Apple Developer Program 会员仍可使用 Xcode 的个人免费签名进行有限的个人测试，但通常需要 Mac、Apple ID，并且安装有效期/设备数量等有约束。
- 不存在一种通用、官方、完全不签名且可直接安装到所有 iPhone 的原生 IPA 方案。
- 如果没有 Mac、没有付费签名，建议先用 Safari 添加到主屏幕的 PWA 方案。

## 游戏功能说明
- 网页代码中有单人模式，因此单人模式不需要联机服务器。
- 多人联机需要有可从手机访问的 Socket.IO 游戏服务器和正确配置的 IP/端口。仅把客户端封装成 APK 不会自动创建联机服务器。
- 该游戏使用 WebGL/Three.js；实际手机性能、触控操作和 WebGL 支持需要在真机测试。
- PWA 离线缓存只缓存主要本地游戏文件；外部字体和联机功能仍需要网络。


## 手机触控（已添加）
- 左下虚拟摇杆：W/A/S/D 移动（开车时对应油门、倒车和转向）。
- 右侧透明区域：滑动旋转视角。
- ATTACK：攻击/射击；USE：交互；CAR：进入/离开车辆或触发原游戏对应动作。
- JUMP：按住空格键对应动作（开车时可作为手刹）；RUN：按住 Shift；RELOAD：换弹；PAUSE：暂停。
- 控件只在触屏/窄屏设备且游戏开始后显示，桌面鼠标设备默认隐藏。
- 真机测试仍然必要，个别动作的体验可能需要按实际玩法微调。
