const jwt = require("jsonwebtoken");
const TokenBlacklist = require("../models/TokenBlacklist");
const User = require("../models/User");

// Protect middleware to verify token and user
const protect = async (req, res, next) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).json({ message: "Access denied. No token provided." });

  try {
    const blacklisted = await TokenBlacklist.findOne({ token });
    if (blacklisted) {
      return res.status(401).json({ message: "Token is blacklisted. Please login again." });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.id).select("-password");
    if (!user) return res.status(404).json({ message: "User not found." });

    req.user = user;
    next();
  } catch (err) {
    res.status(400).json({ message: "Invalid token." });
  }
};

// isAdmin middleware
const isAdmin = (req, res, next) => {
  if (req.user && req.user.role === "admin") {
    next();
  } else {
    res.status(403).json({ message: "Access denied: Admins only." });
  }
};

module.exports = {
  protect,
  isAdmin,
};
