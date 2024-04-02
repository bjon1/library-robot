import { useState } from 'react';
import RobotAPI from '../../utilities/RobotAPI';

const Movement = () => {

    const [range, setRange] = useState('50');
    const [sliding, setSliding] = useState(false);

    const updateSlider = (value) => {
        setSliding(true);
        setRange(value);
    };

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
            <div className="Movement__Slider" onMouseEnter={() => RobotAPI.setRobotSpeed(parseInt(range) < '10' ? '10' : parseInt(range))}>
                <p className="SliderText">{parseInt(range) + '%'}</p>
                <input
                    type="range"
                    min="0"
                    max="100"
                    value={range}
                    className="slider"
                    onChange={event => updateSlider(event.target.value)}
                />
            </div>
        </>
    )
}

export default Movement