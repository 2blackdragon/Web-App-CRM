import "../../styles/Header.css"
import img from "../../img/image.png"

function Header () {
    return (
        <div className="header">
            <div className="image">
                <img src={img} />
            </div>
            <div>
                <button>Выход</button>
            </div>
        </div>
    )
}


export default Header;