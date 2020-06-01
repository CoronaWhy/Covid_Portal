import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ListStrainsComponent } from './list-strains.component';

const routes: Routes = [
    {
        path: '',
        component: ListStrainsComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ListStrainsRoutingModule {}
