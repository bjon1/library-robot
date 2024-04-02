import { useNavigate, useLocation } from 'react-router-dom';

const Header = () => {

    const navigate = useNavigate();
    const address = useLocation();
    const isOnMainMenu = address.pathname === '/';

    return( 
        <div>
            {!isOnMainMenu && <div className="back-button">
                <i 
                    onClick={() => navigate('/')}
                    className="fa-solid fa-arrow-left"></i>
            </div>}
        </div>
    );

}

export default Header