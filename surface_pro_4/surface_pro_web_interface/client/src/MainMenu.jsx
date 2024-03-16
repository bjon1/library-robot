import MainButtons from './MainButtons.jsx'

const MainMenu = () => {

    const buttons = [
        {
           image: "./imgs/move.png",
           link: "/movement",
           name: "Movement"
        },
        {
           image: "./imgs/diagnostics.png",
           link: "/diagnostics",
           name: "Diagnostics"
        },
        {
           image: "./imgs/smile.png",
           link: "/faces",
           name: "Faces"
        },
        {
           image: "./imgs/camera.jpg",
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