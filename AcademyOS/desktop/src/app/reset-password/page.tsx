import {redirect} from 'next/navigation';
import {liveSupabase} from '@/lib/supabase/config';
import {LoginScreen} from '@/components/login-screen';
import '../login/login.css';
export const metadata={title:'Reset password · AcademyOS'};
export default function Page(){if(!liveSupabase)redirect('/login');return <LoginScreen variant="reset-password" destination="/workspace"/>}
