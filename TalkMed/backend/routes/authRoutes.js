const express = require("express");
const router = express.Router();

const { registerUser, verifyOTP, loginUser, sendLoginOTP, verifyLoginOTP, logout } = require("../controllers/authController");
const { getVerifiedDoctors, getDoctorsByLocation } = require("../controllers/doctorController");
const { protect } = require("../middlewares/authMiddlewares");
const TokenBlacklist = require("../models/TokenBlacklist");

router.post("/register", registerUser);
router.post("/verify-otp", verifyOTP);
router.post("/login", loginUser);

router.post("/login-otp", sendLoginOTP);
router.post("/verify-login-otp", verifyLoginOTP);
router.get("/verified", getVerifiedDoctors);
router.get("/location/:location", getDoctorsByLocation);

router.post("/logout", protect, logout);

module.exports = router;
