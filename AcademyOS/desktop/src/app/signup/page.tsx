import {LoginScreen} from '@/components/login-screen';
import '../login/login.css';
export const metadata={title:'Create your account · AcademyOS',description:'Join your school community with your AcademyOS invitation.'};
export default function Page(){return <LoginScreen destination="/dashboard" variant="signup-choice"/>}
