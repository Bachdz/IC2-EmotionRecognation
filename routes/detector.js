const express = require('express');
const router = express.Router();
const multer = require('multer');
const upload = multer({dest: 'uploads/'});
const path = require('path');

const runDetection = (pathToImage, model) => {
    return new Promise(function (success, nosuccess) {
        try {
            const {spawn} = require('child_process');
            const pyprog = spawn('python', ['main.py',
                '--image', pathToImage,
                '--model', model
                ],{
                cwd: path.resolve(__dirname, "..")
            });

            let output = ""

            pyprog.stdout.on('data', function (data) {
                output += data
            });

            pyprog.stderr.on('data', (data) => {
                output += data
            });

            pyprog.on('close', (code) => {
                console.log(`child process exited with code ${code}`);
                console.log(output)
                success(output)
            });

        } catch (err) {
            nosuccess(err)
        }
    })
};

router.post('/', upload.single('image'), (req, res, next) => {
    try {
        const allowedMimeTypes = ['image/png', 'image/jpeg', 'image/jpeg4', 'image/jpeg']
        const errors = []
        if (!req.file || !allowedMimeTypes.includes(req.file.mimetype)) {
            res.status(400)
            errors.push('Please upload a valid image file. Allowed file types are: png, jpg, jpeg4')
        }

        if(!req.body.model){
            res.status(400)
            errors.push('Please select a model')
        }

        if(errors.length> 0) {
            return res.render('home', {errors})
        }

        runDetection(req.file.path, req.body.model)
        res.render('detection')

    } catch (err) {
        next(err)
    }
});

router.get('/', (req, res) => {
    res.redirect('/')
});

module.exports = router;

