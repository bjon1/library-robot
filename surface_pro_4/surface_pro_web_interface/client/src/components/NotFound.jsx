import { useNavigate} from 'react-router-dom';

const NotFound = () => {

    const navigate = useNavigate();
    const handleClick = () => {
        navigate('/');
    }

return (

        <div>
            <h1>404 Not Found</h1>
            <div>Sorry, this page does not exist!</div>
            <button onClick={handleClick}>Return Home</button>
        </div>

    )
}


export default NotFound;