import {LoginScreen} from '@/components/login-screen';
import {safeDestination} from '@/lib/demo-auth';
import './login.css';
export const metadata={title:'Sign in · AcademyOS',description:'Your school day, beautifully connected. Sign in to your AcademyOS workspace.'};
export default async function Page({searchParams}:{searchParams:Promise<{next?:string}>}){const {next}=await searchParams;return <LoginScreen destination={safeDestination(next)}/>}
