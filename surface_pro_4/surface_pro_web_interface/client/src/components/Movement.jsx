import { useState } from 'react';
import RobotAPI from '../../utilities/RobotAPI';

const Movement = () => {

    const [range, setRange] = useState(50);

    const changeSpeed = (e) => {
        if (e.target.classList.contains('fa-circle-arrow-left')) {
            if (range > 0) {
                setRange(range - 10);
                RobotAPI.setRobotSpeed(range - 10);
            }
        }
        if (e.target.classList.contains('fa-circle-arrow-right')) {
            if (range < 100) {
                setRange(range + 10);
                RobotAPI.setRobotSpeed(range + 10);
            }
        }
    }

    const buttonData = [
        { title: 'Left 90', image: '../imgs/turn-left.png', onPress: () => RobotAPI.turnLeft() },
        { title: 'Forward', image: '../imgs/up.png', onPress: () => RobotAPI.moveForward() },
        { title: 'Right 90', image: '../imgs/turn-right.png', onPress: () => RobotAPI.turnRight() },

        { title: 'CCW', image: '../imgs/CCW.png', onPress: () => RobotAPI.turnCounterClockwise() },
        { title: 'STOP', image: '../imgs/stop.png', onPress: () => RobotAPI.stopRobot() },
        { title: 'CW', image: '../imgs/CW.png', onPress: () => RobotAPI.turnClockwise() },

        { title: 'Reverse', image: '../imgs/down.png', onPress: () => RobotAPI.moveBackward() },

        { title: 'Cruise', image: '../imgs/up.png', onPress: () => RobotAPI.moveForward() },
        { title: 'STOP', image: '../imgs/stop.png', onPress: () => RobotAPI.stopRobot() }
    ];

    return (
        <>
            <div className="Movement">

                <div className="row">
                    {buttonData.slice(0, 3).map((button, index) => (
                        <button key={index} className="button" onClick={button.onPress}>
                            <img src={button.image} className="buttonImage" />
                        </button>
                    ))}
                </div>

                <div className="row">
                    {buttonData.slice(3, 6).map((button, index) => (
                        <button key={index} className="button" onClick={button.onPress}>
                            <img src={button.image} className="buttonImage" />
                        </button>
                    ))}
                </div>

                <div className="row">
                    <button
                        className="button centeredButton"
                        onClick={() => RobotAPI.moveBackward()}
                    >
                        <img src={buttonData.find(button => button.title === 'Reverse').image} className="buttonImage" />
                    </button>
                </div>
            </div>
            <div className="Movement__Slider">
                <i class="fa-solid fa-circle-arrow-left" onClick={changeSpeed}></i>
                <div className="Slider__text">
                    {range}
                </div>
                <i class="fa-solid fa-circle-arrow-right" onClick={changeSpeed}></i>
            </div>
        </>
    )
}

export default Movement