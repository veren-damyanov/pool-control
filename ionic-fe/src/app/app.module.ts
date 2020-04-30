import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

import { CardContentComponent } from './card-content/card-content.component';
import { CardComponent } from './card/card.component';
import { CardContextMenuComponent } from './card-context-menu/card-context-menu.component';
import { FormPopoverComponent } from './form-popover/form-popover.component';
import { SettingsComponent } from './settings/settings.component';
import { DeviceComponent } from './device/device.component';
import { DeviceFormComponent } from './device-form/device-form.component';
import { DeviceItemComponent } from './device-item/device-item.component';
import { DeviceContextMenuComponent } from './device-context-menu/device-context-menu.component';
import { AboutComponent } from './about/about.component';
import { PinoutComponent } from './pinout/pinout.component';
import { DeviceService } from './device.service';

@NgModule({
	declarations: [AppComponent,
		CardContentComponent,
		CardComponent,
		CardContextMenuComponent,
		FormPopoverComponent,
		SettingsComponent,
		DeviceComponent,
		DeviceFormComponent,
		DeviceItemComponent,
		DeviceContextMenuComponent,
		AboutComponent,
		PinoutComponent,
	],
	entryComponents: [CardContextMenuComponent,
		FormPopoverComponent,
		DeviceFormComponent,
		DeviceContextMenuComponent,
	],
	imports: [
		BrowserModule,
		IonicModule.forRoot(),
		AppRoutingModule,
		HttpClientModule,
		FormsModule,
		ReactiveFormsModule
	],
	providers: [
		StatusBar,
		SplashScreen,
		DeviceService,
		{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy }
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
