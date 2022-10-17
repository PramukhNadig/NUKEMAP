function Cloud(radius, x, y, vx, vy, growth) {
  this.radius = radius;
  this.x = x;
  this.y = y;
  this.vx = vx;
  this.vy = vy;
  this.growth = growth;
}

function Ground(width, height, interval, cloud) {
  this.width = width;
  this.height = height;
  this.interval = interval;
  this.cloud = cloud;
  this.positions = [[this.cloud.x, this.cloud.y]];
  this.position = 0;
}

Ground.prototype.drawCloud = async function () {
  let c = document.getElementById("myCanvas");
  c.setAttribute("width", this.width);
  c.setAttribute("height", this.height);
  let ctx;

  if (c.getContext) {
    ctx = c.getContext("2d");
  }

  let length = Math.sqrt(
    this.positions[this.position][0] * this.positions[this.position][0] +
      this.positions[this.position][1] * this.positions[this.position][1]
  );
  let vx = this.positions[this.position][0] / length;
  let vy = this.positions[this.position][1] / length;

  while (
    this.positions[this.position][0] < this.width &&
    this.positions[this.position][1] < this.height
  ) {
    ctx.beginPath();
    ctx.arc(
      this.positions[this.position][0],
      this.positions[this.position][1],
      this.cloud.radius,
      0,
      2 * Math.PI
    );
    ctx.stroke();
    if (this.position > 0) {
      ctx.beginPath();
      ctx.arc(
        this.positions[this.position - 1][0],
        this.positions[this.position - 1][1],
        this.cloud.radius / this.cloud.growth,
        0,
        2 * Math.PI
      );
      ctx.fill();
    }

    this.positions.push([
      this.positions[this.position][0] + vx * 20,
      this.positions[this.position][0] + vy * 20,
    ]);
    this.position++;
    this.cloud.radius = this.cloud.radius * this.cloud.growth;
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
};

let cloud = new Cloud(5, 10, 10, 1, 1, 1.05);
let ground = new Ground(500, 500, 1, cloud);

ground.drawCloud();
