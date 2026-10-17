import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.xstudio.neonharbor',
  appName: 'Neon Harbor',
  webDir: 'www',
  bundledWebRuntime: false,
  backgroundColor: '#070b14',
  android: {
    allowMixedContent: true
  },
  ios: {
    contentInset: 'automatic'
  }
};

export default config;
