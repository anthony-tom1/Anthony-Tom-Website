function makeCanvas () {
	let canvas = document.createElement("canvas");
	canvas.width = 400;
	canvas.height = 400;
	canvas.style.border = "2px dashed black";
    
    document.addEventListener("DOMContentLoaded", function() {
        document.body.appendChild(canvas);
    });
	canvas.ctx = canvas.getContext("2d");
	return canvas;
}

class DisplayObject {
	constructor() {
		this.x = 0;
		this.y = 0;
		this.width = 0;
		this.height = 0;
		this.circular = false;
		
		this.children = [];
		this.parent = undefined;
	}
	
	addChild(sprite) {
		sprite.parent = this;
		this.children.push(sprite);
	}
	
	removeChild(sprite) {
		if (sprite.parent == this) {
			this.children.splice(this.children.indexOf(sprite), 1);
		}
	}
}

let stage = new DisplayObject;

function render(canvas) {
	canvas.ctx.clearRect(0, 0, 400, 400);
	stage.children.forEach( (sprite) => { displaySprite(sprite); } );
	
	function displaySprite(sprite) {
		sprite.draw(canvas.ctx);
	}
}

class Rectangle extends DisplayObject {
	constructor(x = 50, y = 100, width = 50, height = 20) {
		super();
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
	}
	
	draw(ctx) {
		ctx.beginPath();
		ctx.rect(this.x, this.y, this.width, this.height);
        ctx.fillStyle = "gray";
        ctx.strokeStyle = "black";
           
        ctx.fill();
        ctx.stroke();
	}
}

function rectangle(x, y, width, height) {
	let sprite = new Rectangle(x, y, width, height);
	stage.addChild(sprite);
	console.log(stage);
	return sprite;
}

class Circle extends DisplayObject {
	constructor(x = 25, y = 25, diameter = 40) {
		super();
		this.x = x;
		this.y = y;
		this.circular = true;
		this.diameter = diameter;
		this.radius = diameter / 2;
		this.width = diameter;
		this.height = diameter;
	}
	
	draw(ctx) {
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.radius, 0, 2*Math.PI)
		ctx.stroke();
	}
}

function circle(x, y, diameter) {
	let sprite = new Circle(x, y, diameter);
	stage.addChild(sprite);
	return sprite;
}

class Dot extends DisplayObject {
	constructor(x = 25, y = 25, diameter = 40, hue = 0) {
		super();
		this.x = x;
		this.y = y;
		this.circular = true;
		this.diameter = diameter;
		this.radius = diameter / 2;
		this.width = diameter;
		this.height = diameter;
		this.lightness = 25;
		this.fillStyle = "black"
		
	}
	
	draw(ctx) {
		ctx.beginPath();
		//ctx.fillStyle = this.fillStyle;
		ctx.fillStyle = "hsl("+ this.hue + ", 100%, "+ this.lightness + "%)"
		ctx.arc(this.x, this.y, this.radius, 0, 2*Math.PI)
		ctx.fill();
		
		this.lightness += 1;
		if (this.lightness >= 75) {
			this.lightness = 25;
		}
		
		ctx.fillStyle = "black";
	}
}

function dot(x, y, diameter) {
	let sprite = new Dot(x, y, diameter);
	stage.addChild(sprite);
	return sprite;
}

class TrafficLight extends DisplayObject {
	constructor(x = 25, y = 25, diameter = 40, hue = 0) {
		super();
		this.x = x;
		this.y = y;
		this.circular = true;
		this.diameter = diameter;
		this.radius = diameter / 2;
		this.width = diameter;
		this.height = diameter;
		this.hue = hue;
		this.lightness = 25;
		this.fillStyle = "black";
		this.anim = true;
        this.on = false;
		
	}
	
	draw(ctx) {
		ctx.beginPath();
		//ctx.fillStyle = this.fillStyle;
		ctx.fillStyle = "hsl("+ this.hue + ", 100%, "+ this.lightness + "%)"
		ctx.arc(this.x, this.y, this.radius, 0, 2*Math.PI);
		ctx.fill();
		
		this.switchLight();
		
		ctx.fillStyle = "black";
	}
	
	switchLight() { /* For &&, put both conditions in one (). Do not put the conditions in separate parentheses. */
        if (this.on === true) {
            this.lightness += 1;
            if (this.lightness > 65) { 
                this.lightness = 65;
            }
		} else if (this.on === false) {
            this.lightness -= 1;
            if (this.lightness < 0) { 
                this.lightness = 0;
            }
        }
	}
}

function trafficLight(x, y, diameter, hue) {
	let sprite = new TrafficLight(x, y, diameter, hue);
	stage.addChild(sprite);
	return sprite;
}