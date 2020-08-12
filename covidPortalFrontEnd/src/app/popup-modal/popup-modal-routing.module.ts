import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PopupModalComponent } from './popup-modal.component';

const routes: Routes = [
    {
        path: '', component: PopupModalComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class PopupModalRoutingModule {
}
