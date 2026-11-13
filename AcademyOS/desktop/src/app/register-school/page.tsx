import {LoginScreen} from '@/components/login-screen';
import '../login/login.css';
import './registration.css';
export const metadata={title:'Register your school · AcademyOS',description:'Create your school owner preview and begin guided school setup.'};
export default function Page(){return <LoginScreen destination="/setup" variant="register-school"/>}
