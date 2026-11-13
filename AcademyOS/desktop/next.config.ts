import type {NextConfig} from 'next';
const config:NextConfig={
 devIndicators:false,
 async headers() {
  return ['/fonts/:path*', '/landing-pages/aura-2026-10-27-assets/:path*'].map(source => ({
   source, headers: [{key:'Access-Control-Allow-Origin',value:'*'}],
  }));
 },
 // Let browser checks run without sharing the active developer server's cache.
 distDir:process.env.ACADEMYOS_ISOLATED_PREVIEW==='1'?'.next-preview':'.next',
};
export default config;
