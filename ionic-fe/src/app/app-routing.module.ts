import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

import { CardContentComponent } from './card-content/card-content.component';
import { SettingsComponent } from './settings/settings.component';
import { DeviceComponent } from './device/device.component';
import { AboutComponent } from './about/about.component';
import { PinoutComponent } from './pinout/pinout.component';

const routes: Routes = [
	// {
	// 	path: 'folder/:id',
	// 	loadChildren: () => import('./folder/folder.module').then(m => m.FolderPageModule)
	// },
	{
		path: '',
		redirectTo: 'schedule',
		pathMatch: 'full'
	},
	{
		path: 'schedule',
		component: CardContentComponent
	},
	{
		path: 'settings',
		component: SettingsComponent
	},
	{
		path: 'devices',
		component: DeviceComponent
	},
	{
		path: 'about',
		component: AboutComponent
	},
	{
		path: 'pinout',
		component: PinoutComponent
	},
];

@NgModule({
	imports: [
		RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
	],
	exports: [RouterModule]
})
export class AppRoutingModule { }
