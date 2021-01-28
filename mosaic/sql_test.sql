-- Given tables
-- Employee
-- +----+-------+--------+--------------+
-- | Id | Name  | Salary | DepartmentId |
-- +----+-------+--------+--------------+
-- | 1  | Joe   | 70000  | 1            |
-- | 2  | Henry | 80000  | 2            |
-- | 3  | Sam   | 60000  | 2            |
-- | 4  | Max   | 90000  | 1            |
-- +----+-------+--------+--------------+
-- and
-- Department
-- +----+----------+
-- | Id | Name     |
-- +----+----------+
-- | 1  | IT       |
-- | 2  | Sales    |
-- +----+----------+
-- Find the name and dept name of person from each dept with highest salary
-- Author: John Feilmeier

with max_salary_per_dept as (
    select DepartmentId, max(Salary) as Salary
    from Employee
    group by DepartmentId
);
select e.Name as employee_name, d.Name as department_name
from Department d
join max_salary_per_dept m on m.DepartmentId = d.Id
join Employee e on e.Salary = m.Salary
;
