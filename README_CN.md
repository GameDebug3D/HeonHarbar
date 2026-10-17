# Neon Harbor 手机应用项目

## 当前应用配置
- 桌面显示名称：`Neon Harbor`
- Android 应用包名：`com.neonharbor.game`
- 构建类型：Android Debug APK（用于安装测试）
- 网页入口：`www/index.html`
- 封装框架：Capacitor 6
- Java：17；Node.js：20

主要配置文件：
- `capacitor.config.ts`：应用名称、包名和 Web 资源目录。
- `package.json`：Capacitor 依赖和常用命令。
- `.github/workflows/build-android.yml`：GitHub Actions 自动构建流程。
- `.gitignore`：忽略生成的 Android/iOS 工程和依赖目录。

## 通过 GitHub 自动编译 APK（推荐）

1. 下载并解压本项目 ZIP。
2. 在 GitHub 新建一个仓库，例如 `NeonHarbor-Mobile`。
3. 将解压后的**所有文件和文件夹**上传到仓库根目录。确认 `.github/workflows/build-android.yml` 也已上传；`.github` 是隐藏目录，不能漏掉。
4. 打开 GitHub 仓库的 **Actions** 页面。如果出现提示，点击启用 Actions。
5. 在左侧选择 **Build Neon Harbor Android Debug APK**。
6. 点击 **Run workflow**，选择 `main` 或 `master` 分支，再点击绿色的 **Run workflow**。
7. 打开最新一次运行记录，等待所有步骤显示绿色勾号。
8. 在运行记录页面底部的 **Artifacts** 区域，下载 `NeonHarbor-Android-debug`。
9. 解压下载的 Artifact，得到 `app-debug.apk`，将 APK 传到安卓手机后打开安装。手机可能需要允许该来源安装应用。

也可以把更新推送到 `main` 或 `master` 分支，工作流会自动运行。

## 本地构建（可选）
需要安装 Node.js 20、Java JDK 17 和 Android SDK。然后在项目根目录运行：

```bash
npm install
npx cap add android
npx cap sync android
cd android
./gradlew assembleDebug
```

Windows PowerShell 最后一步使用：

```powershell
.\gradlew.bat assembleDebug
```

生成的 APK 通常位于 `android/app/build/outputs/apk/debug/app-debug.apk`。

## 重要说明
- 本 ZIP 已准备好配置和自动编译工作流，但当前环境没有实际运行 GitHub Actions，因此**尚未产出经过真机安装验证的 APK**。首次编译需在 GitHub Actions 或已配置 Android SDK 的电脑上执行。
- Debug APK 用于测试，不是 Google Play 商店发布包；它不需要你预先提供正式发布签名密钥。
- `com.neonharbor.game` 是 Android 应用唯一标识，若未来发布到商店，建议保持不变。
- 手机触控已加入网页层：左下虚拟摇杆、右侧视角拖动和动作按钮。请在真机上验证控制映射、画面比例和性能。
- 游戏单人模式不需要联机服务器；多人模式仍需要手机可访问的 Socket.IO 服务端。
- iPhone 原生 App 需要 macOS/Xcode 进行构建和签名。没有 Mac 时可先通过 Safari 将网页添加到主屏幕，作为 PWA 使用。

## 目录结构

```text
NeonHarbor_MobileApp/
├── .github/workflows/build-android.yml
├── .gitignore
├── capacitor.config.ts
├── package.json
├── README_CN.md
├── www/
│   ├── index.html
│   ├── manifest.webmanifest
│   ├── sw.js
│   ├── three.min.js
│   ├── socket.io.min.js
│   └── icons/
└── desktop-original/   # 原 Python 启动器和日志备份
```


### GitHub Actions 锁文件报错修复
如果 `actions/setup-node@v4` 报错找不到 `package-lock.json`，请确保工作流的 `Set up Node.js` 步骤只配置 `node-version: 20`，不要配置 `cache: npm`。项目未提交 npm 锁文件时，移除缓存选项即可。


### 构建依赖修复
项目已将 TypeScript 加入 devDependencies，工作流也会在生成 Android 工程前确保 TypeScript 已安装，以支持 capacitor.config.ts。


### 手机画面显示修复（Fixed3）
- 已将触控控件 CSS 正确包在 `<style>` 标签中，避免样式被浏览器当作正文显示。
- GitHub Actions 会在生成 Android 工程后自动修改启动 Activity 的 `screenOrientation` 为 `landscape`，让 Android App 启动时使用横屏。
- 横屏设置适用于本项目构建出来的 Android APK；手机浏览器打开网页时，是否允许自动锁定横屏取决于浏览器和系统权限。


## 重要：手机界面与全屏修复版
此版本进一步调整了手机横屏界面：移动端菜单改为全屏布局、缩小 HUD/小地图、缩小虚拟摇杆和动作按钮，并增强触屏设备识别。Android 工作流还会修改原生 MainActivity，设置横屏并启用沉浸式全屏（隐藏状态栏/导航栏）。

请将本 ZIP 的 `www/index.html` 和 `.github/workflows/build-android.yml` 更新到 GitHub 仓库，再重新运行 Actions 生成新的 APK。旧 APK 不会自动更新。浏览器网页/PWA 无法强制隐藏系统状态栏；沉浸式全屏设置只作用于重新编译后的 Android 原生 APK。真机仍需测试。


## 网页直接适配修复（v4）
本版本直接修改 `www/index.html`：追加最终优先级的手机 UI CSS、缩放主菜单/HUD/触控按钮、添加网页全屏/横屏尝试按钮，并更新缓存版本。浏览器是否允许全屏/横屏锁定取决于平台；Capacitor 原生沉浸式状态栏仍需 Android 原生配置配合。
