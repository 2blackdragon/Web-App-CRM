import "../../styles/LoginUser.css"
import api from "../Api"
import { useRef } from "react"
import { useNavigate } from 'react-router-dom';


function LoginUser () {
    const navigate = useNavigate();

    const navigateHomePage = () => {
        navigate('/');
    };

    const save_user_data = async (name, surname) => {

        const user_id = await api.get("/get_user_id", {"name": name, "surname": surname})

        localStorage.setItem("isLoggedIn", true);
        localStorage.setItem("userId", user_id);
    }

    const post_user = async (event) => {
        event.preventDefault();
        const name = name_ref.current.value;
        const surname = surname_ref.current.value;
        await api.post("/login", {"name": name, 
                                  "surname": surname, 
                                  "is_master": false}).then(function (response){
                                    console.log(response);
                       })

        save_user_data(name, surname);

        navigateHomePage();
    }

    const name_ref = useRef();
    const surname_ref = useRef();

    return (
        <div className="login_div">
            <h1>Вход</h1>
            <form className="login_form" onSubmit={post_user}>
                <input type="text" defaultValue="Имя" className="fullname" ref={name_ref} />
                <input type="text" defaultValue="Фамилия" className="fullname" ref={surname_ref} />
                <input type={"submit"} value="Войти" className="submit" />
            </form>
        </div>
    )
}

export default LoginUser;