
/* Endpoints:
*  - /api/robot/move-forward
*  - /api/robot/move-backward
*  - /api/robot/turn-left
*  - /api/robot/turn-right
*  - /api/robot/turn-clockwise
*  - /api/robot/turn-counter-clockwise
*  - /api/robot/stop-robot
*  - /api/robot/status
*/

import express from 'express'
import model from '../models/robot.js'

const router = express.Router()

router
    .post('/move-forward', async (req, res, next) => {
        try {
            const response = await model.moveForward()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .post('/move-backward', async (req, res, next) => {
        try {
            const response = await model.moveBackward()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .post('/turn-left', async (req, res, next) => {
        try {
            const response = await model.turnLeft()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .post('/turn-right', async (req, res, next) => {
        try {
            const response = await model.turnRight()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .post('/turn-clockwise', async (req, res, next) => {
        try {
            const response = await model.turnClockwise()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .post('/turn-counter-clockwise', async (req, res, next) => {
        try {
            const response = await model.turnCounterClockwise()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .post('/stop-robot', async (req, res, next) => {
        try {
            const response = await model.stopRobot()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .post('/set-speed', async (req, res, next) => {
        try {
            let speed = req.body.speed
            speed = Math.max(Math.min(100, speed), 10)
            const response = await model.setRobotSpeed(speed)
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

    .get('/status', async (req, res, next) => {
        try {
            const response = await model.getRobotStatus()
            res.json(response)
        } catch (error) {
            next(error)
        }
    })

export default router