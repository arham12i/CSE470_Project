const mongoose = require("mongoose");

const tokenBlacklistSchema = new mongoose.Schema({
  token: { type: String, required: true, unique: true },
  blacklistedAt: { type: Date, default: Date.now, expires: '1d' }, // Auto-remove after 1 day
});

module.exports = mongoose.model("TokenBlacklist", tokenBlacklistSchema);
