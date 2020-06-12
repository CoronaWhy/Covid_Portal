import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TestDatatableComponent } from './test-datatable.component';

const routes: Routes = [
    {
        path: '',
        component: TestDatatableComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class TestDatatableRoutingModule {}
