import { Component, OnInit, Input } from '@angular/core';
import { PopoverController } from '@ionic/angular';
import { CardContextMenuComponent } from '../card-context-menu/card-context-menu.component';
import { gnotify } from '../events';
import { Content } from '@angular/compiler/src/render3/r3_ast';

@Component({
	selector: 'app-card',
	templateUrl: './card.component.html',
	styleUrls: ['./card.component.scss'],
})
export class CardComponent implements OnInit {

	@Input() record;
	@Input() inUse;
	private notify = gnotify;
	private popover = null;

	constructor(public popoverController: PopoverController) {
	}

	ngOnInit() { }

	async presentContextPopover(ev: any) {
		console.info("presentContextPopover() creating card context menu")
		const popover = await this.popoverController.create({
			component: CardContextMenuComponent,
			componentProps: { 'record': this.record, 'inUse': this.inUse },
			event: ev,
			translucent: true
		});
		// this.popover = popover;
		return await popover.present();
	}

	padTime(num) {
		console.debug("padTime() called")
		return ("00" + num).slice(-2)
	}

	formatTime(time) {
		console.debug("formatTime() called")
		// '1990-02-19T08:00+02:00'
		var hour = +time.slice(11, 13);
		var minute = +time.slice(14, 16);
		var qualifier = 'AM';

		if (hour == 0) {
			hour = 12;
		} else if (hour == 12) {
			qualifier = 'PM';
		} else if (hour >= 13) {
			hour = hour - 12;
			qualifier = 'PM';
		}
		return (this.padTime(hour) + ':' + this.padTime(minute) + ' ' + qualifier)
	}
}
