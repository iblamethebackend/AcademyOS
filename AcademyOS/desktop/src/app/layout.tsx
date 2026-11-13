import type {Metadata} from 'next';
import './globals.css';
import 'lenis/dist/lenis.css';
import './motion.css';
import {AppMotion} from '@/components/app-motion';
export const metadata:Metadata={title:'AcademyOS \u00b7 Campus management',description:'A smarter campus. A more connected school day.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><AppMotion/>{children}</body></html>}
