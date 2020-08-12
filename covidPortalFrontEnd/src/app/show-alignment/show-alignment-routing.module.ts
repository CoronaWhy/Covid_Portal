import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ShowAlignmentComponent } from './show-alignment.component';

const routes: Routes = [
    {
        path: '',
        component: ShowAlignmentComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ShowAlignmentRoutingModule {}
