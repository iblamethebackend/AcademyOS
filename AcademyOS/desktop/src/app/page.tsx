import type {Metadata} from 'next';
import {FormaAiLandingPage} from '@/components/forma-ai-landing-page';
export const metadata:Metadata={title:'AcademyOS · A smarter campus',description:'A connected school workspace. Explore available foundations and the AcademyOS roadmap for learning, operations and mobile.'};
export default function Home(){return <FormaAiLandingPage/>}
