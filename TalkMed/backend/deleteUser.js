const mongoose = require("mongoose");
const User = require("./models/User");
require("dotenv").config();

mongoose.connect(process.env.MONGO_URI)
  .then(async () => {
    await User.deleteOne({ email: "shawon12hssain@gmail.com" });
    console.log("User deleted");
    process.exit(0);
  })
  .catch(err => {
    console.error(err);
    process.exit(1);
  });