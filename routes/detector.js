const express = require('express');
const router = express.Router();
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

router.post('/', upload.single('image'),(req, res) => {
    res.send("POST detector");
});


module.exports = router;

