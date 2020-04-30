import { Component, OnInit, Input } from '@angular/core';
import { ModalController, PopoverController } from '@ionic/angular';

import { RecordService } from '../record.service';
import { FormPopoverComponent } from '../form-popover/form-popover.component';
import { gnotify } from '../events';


@Component({
	selector: 'app-card-context-menu',
	templateUrl: './card-context-menu.component.html',
	styleUrls: ['./card-context-menu.component.scss'],
})
export class CardContextMenuComponent implements OnInit {

	private notify = gnotify;
	private record;
	private inUse;

	constructor(private recordService: RecordService, public popoverController: PopoverController, public modalController: ModalController) { }

	ngOnInit() { }

	deleteRecord() {
		console.debug("deleteRecord() called")
		this.recordService.deleteRecord(this.record.pkey).subscribe(data => {
		}, err => {
			console.error('Delete record failed.', err)
		});
		this.notify.emit('reload');
		this.popoverController.dismiss()
	}

	async presentFormModal() {
		console.info("presentFormModal() creating form modal from context menu")
		const modal = await this.modalController.create({
			component: FormPopoverComponent,
			componentProps: { 'record': this.record, 'operation': 'edit', 'inUse': this.inUse }
		});
		var result = await modal.present();
		this.popoverController.dismiss()
		return result
	}
}
