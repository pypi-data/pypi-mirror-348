from odoo import api, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for vals, task in zip(vals_list, tasks):
            if "date_deadline" in vals:
                task.update_parent_task_dates()
        return tasks

    def write(self, vals):
        res = super().write(vals)
        if "date_deadline" in vals or "stage_id" in vals:
            self.update_parent_task_dates()
        return res

    def update_parent_task_dates(self):
        for task in self:
            parent = task.parent_id
            if parent:
                children = parent.child_ids.filtered(
                    lambda child: not child.stage_id.fold and child.date_deadline
                )
                deadline = children and min(children.mapped("date_deadline"))
                if deadline and parent.date_deadline != deadline:
                    parent.date_deadline = deadline
