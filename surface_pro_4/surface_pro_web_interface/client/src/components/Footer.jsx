import { useNavigate, useLocation } from 'react-router-dom';

const Footer = () => {

    const navigate = useNavigate();
    const address = useLocation();
    const isOnMainMenu = address.pathname === '/';

    return(
        
        <div className="footer">
            <img className="footer_stop" src="../../img/stop.png" />
            <p>&copy; {new Date().getFullYear()} SD2024</p>
            {isOnMainMenu && 
                <img 
                    className="footer_admin" 
                    src="../../img/admin-tools.png" 
                    onClick={() => navigate('/admin')}
                />
            }
        </div>
   
    );

}
export default Footer