import MainButtons from './MainButtons.jsx'

const MainMenu = () => {

    const buttons = [
        {
           image: "./img/move.png",
           link: "/movement",
           name: "Movement"
        },
        {
           image: "./img/diagnostics.png",
           link: "/diagnostics",
           name: "Diagnostics"
        },
        {
           image: "./img/smile.png",
           link: "/faces",
           name: "Faces"
        },
        {
           image: "./img/camera.jpg",
           link: "/viewcameras",
           name: "View cameras"
        }
    ]

    return (
        <div className="MainMenu">
            {buttons.map((button, key) => (
                <MainButtons key={key} image={button.image} link={button.link} name={button.name} />
            ))}
        </div>
    );
}

export default MainMenu