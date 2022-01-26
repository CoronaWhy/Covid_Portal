import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LayoutComponent } from './layout.component';

const routes: Routes = [
    {
        path: '',
        component: LayoutComponent,
        children: [
            { path: '', redirectTo: 'home-page' },
            { path: 'dashboard', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule) },
            // { path: 'report/:fileId', loadChildren: () => import('./report/report.module').then(m => m.ReportModule) },
            { path: 'datafile-detail/:cellId', loadChildren: () => import('./datafile-detail/datafile-detail.module').then(m => m.DatafileDetailModule) },
            { path: 'list-datafiles', loadChildren: () => import('./list-datafiles/list-datafiles.module').then(m => m.ListDatafilesModule) },
            { path: 'show-alignment', loadChildren: () => import('./show-alignment/show-alignment.module').then(m => m.ShowAlignmentModule) },
        ]
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class LayoutRoutingModule {}
