import { Component, OnInit, Input } from '@angular/core';
import { PopoverController } from '@ionic/angular';
import { DeviceContextMenuComponent } from '../device-context-menu/device-context-menu.component';

@Component({
	selector: 'app-device-item',
	templateUrl: './device-item.component.html',
	styleUrls: ['./device-item.component.scss'],
})
export class DeviceItemComponent implements OnInit {

	@Input() device;
	@Input() available;

	constructor(public popoverController: PopoverController) { }

	ngOnInit() { }

	async presentContextPopover(ev: any) {
		console.info("presentContextPopover() creating device context menu")
		const popover = await this.popoverController.create({
			component: DeviceContextMenuComponent,
			componentProps: { 'device': this.device, 'available': this.available },
			event: ev,
			translucent: true
		});
		return await popover.present();
	}

}
