const express = require("express");
const router = express.Router();

const { registerAdmin, loginAdmin, getDashboard, getAllDoctors } = require("../controllers/adminController");
const adminMiddlewares = require("../middlewares/adminMiddlewares");
const { protect, isAdmin } = require("../middlewares/authMiddlewares");
const { verifyDoctor } = require("../controllers/doctorController");

router.post("/register", registerAdmin);
router.post("/login",protect, isAdmin, loginAdmin);

router.get("/dashboard", protect, adminMiddlewares, getDashboard);

router.get("/doctors", protect, adminMiddlewares, getAllDoctors);
router.put("/verify/:id", isAdmin, verifyDoctor);
router.patch("/doctors/:doctorId/verify", protect, adminMiddlewares, verifyDoctor);

module.exports = router;
