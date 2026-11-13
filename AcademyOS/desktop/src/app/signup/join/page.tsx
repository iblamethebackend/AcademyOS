import {LoginScreen} from '@/components/login-screen';
import '../../login/login.css';
export const metadata={title:'Join your school · AcademyOS'};
export default function Page(){return <LoginScreen destination="/dashboard" variant="signup"/>}
