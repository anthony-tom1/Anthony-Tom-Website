function makePointer(element, scale = 1) {
	let pointer = {
		element: element,
		scale: scale,
		x: 0,
		y: 0,
		downTime: 0,
		elapsedTime: 0,
		isUp: true,
		isDown: false,
		tapped: false,
		
		press: undefined,
		release: undefined,
		tap: undefined,
		
		moveHandler(event) {
			let element = event.target;
			this.x = event.pageX - element.offsetLeft;
			this.y = event.pageY - element.offsetTop;
			event.preventDefault();
		},
		
		downHandler(event) {
			this.downTime = Date.now();
			this.isUp = false;
			this.isDown = true;
			this.tapped = false;
			if(this.press) this.press();
			event.preventDefault();
		},
		
		upHandler(event) {
			this.elapsedTime = Math.abs(this.downTime - Date.now());
			if(this.elapsedTime <= 200 && this.tapped == false) {
				this.tapped = true;
				if(this.tap) this.tap();
			}
			this.isUp = true;
			this.isDown = false;
			if (this.release) this.release();
			event.preventDefault();
		},
		
		hitTestSprite(sprite) {
			let hit = false;
			if(!sprite.circular) {
				let left = sprite.x, right = sprite.x + sprite.width, top = sprite.y, bottom = sprite.y + sprite.height;
				hit = (this.x > left && this.x < right && this.y > top && this.y < bottom);
			} else {
				let vx = this.x - sprite.x,
						vy = this.y - sprite.y,
						distance = Math.sqrt(vx*vx + vy*vy);
				console.log("Distance: "+ distance);
				console.log("Radius: "+ sprite.radius);
				hit = distance < sprite.radius;
			}
			return hit;
		}
	} //end let pointer
		
		element.addEventListener("mousemove", pointer.moveHandler.bind(pointer), false);
		element.addEventListener("mousedown", pointer.downHandler.bind(pointer), false);
		window.addEventListener("mouseup", pointer.upHandler.bind(pointer), false);
		element.style.touchAction = "none";
		return pointer;
}
	
function testPointer(pointer, outputText) {
	outputText.innerHTML =
		`Pointer properties: <br>
		pointer.x: ${pointer.x} <br>
		pointer.y: ${pointer.y} <br>
		pointer.isUp: ${pointer.isUp} <br>
		pointer.isDown: ${pointer.isDown} <br>
		pointer.tapped: ${pointer.tapped}`;
}