import express from "express";
import bodyParser from "body-parser";
import fs from "fs";

const app = express();
app.use(bodyParser.json());

// local data storage
const DB = "./airdata.json";

app.post("/api/airdata", (req, res) => {
  const entry = {
    time: Date.now(),
    ...req.body
  };

  let data = [];
  if (fs.existsSync(DB)) {
    data = JSON.parse(fs.readFileSync(DB));
  }

  data.push(entry);
  
  fs.writeFileSync(DB, JSON.stringify(data, null, 2));
  res.json({ status: "ok" });
});

app.get("/api/latest", (req, res) => {
  if (!fs.existsSync(DB)) return res.json({});
  const data = JSON.parse(fs.readFileSync(DB));
  res.json(data[data.length - 1]);
});

app.listen(3000, () => console.log("API running on port 3000"));
