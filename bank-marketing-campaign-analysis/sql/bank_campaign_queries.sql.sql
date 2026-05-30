--Count total rows in the daataset
select count(*) as Total_Customers
from BankCD ;


-- Calculate how many subscribed vs not 
select 
 deposit  as subscriptin_status,
 count(*) as customer_count,
round (count(*) * 100.0/ sum (count(*)) over(), 2 ) as  "percentage"
 from BankCD 
 Group by deposit
 order by customer_count desc;



--Subscription rate per jop type 
select
job,
count(*) as total_in_job,
sum (case when deposit = 'yes' then 1 else 0 end) as subscribed,
round(sum (case when deposit = 'yes' then 1 else 0 end) *100/count(*), 2) as subscription_rate_pct
from BankCD
group by job
order by subscription_rate_pct desc;


-- Subscription rate by month
select
month,
count(*) as total_in_month,
sum (case when deposit = 'yes' then 1 else 0 end) as subscribed,
round(sum (case when deposit = 'yes' then 1 else 0 end) *100/count(*), 2) as subscription_rate_pct
from BankCD
group by month
order by subscription_rate_pct desc;


--How housing loan affects subscription rate
select
housing as housing_loan,
count(*) as total,
sum (case when deposit = 'yes' then 1 else 0 end) as subscribed,
round(sum (case when deposit = 'yes' then 1 else 0 end) *100/count(*), 2) as subscription_rate_pct
from BankCD
group by housing
order by subscription_rate_pct desc;


-- Previous campaign outcome impact

select
poutcome as previous_outcome,
count(*) as total,
sum (case when deposit = 'yes' then 1 else 0 end) as subscribed,
round(sum (case when deposit = 'yes' then 1 else 0 end) *100/count(*), 2) as subscription_rate_pct
from BankCD
group by poutcome
order by subscription_rate_pct desc;


--Conversion rate drops after 3 contacts

select 
campaign as #calls,
count(*) Total_customers,
sum(case when deposit = 'yes' then 1 else 0 end) as supscribed,
round(sum(case when deposit = 'yes' then 1 else 0 end) * 100 / count(*), 2)as supscription_rate_pct
from BankCD
Where campaign<=10
group by campaign 
order by supscription_rate_pct desc;


--Create balance segment and measure conversion
select
   case
       when balance < 0 then '1-Negative'
	   when balance between 0 and 500 then'2-Low'
	   when balance between 501 and 1500 then '3-Medium'
	   when balance between 1501 and 5000 then '4-High'
	   else '5-Very High'
   end as balance_segment,
   count(*) as total,
   sum(case when deposit = 'yes' then 1 else 0 end) as supscribed,
   round(sum(case when deposit = 'yes' then 1 else 0 end) * 100 / count(*), 2)as supscription_rate_pct
from BankCD
group by
     case
         when balance < 0 then '1-Negative'
	     when balance between 0 and 500 then'2-Low'
	     when balance between 501 and 1500 then '3-Medium'
	     when balance between 1501 and 5000 then '4-High'
	     else '5-Very High'
     end
order by balance_segment;


-- Compare avg call duration for yes vs no
select 
deposit,
round (avg(duration) / 60.0,2) AS Avg_Duration_Minutes,
MIN(duration) / 60 AS Min_Duration_Minutes,
MAX(duration) /60  AS Max_Duration_Minutes
FROM BankCD
GROUP BY deposit;



--Create age group and measure conversion
select 
    case
	    when age <= 25 then '18-25'
		when age <= 35 then '26-35'
		when age <= 45 then '36-45'
        when age <= 55 then '46-55'
        when age <= 65 THEN '56-65'
        else '65+'
    end as age_group,
	count(*) as total,
	sum(case when deposit = 'yes' then 1 else 0 end) as supscribed,
	round(sum(case when deposit = 'yes' then 1 else 0 end) * 100 / count(*), 2)as supscription_rate_pct
from BankCD
group by 
      case
	    when age <= 25 then '18-25'
		when age <= 35 then '26-35'
		when age <= 45 then '36-45'
        when age <= 55 then '46-55'
        when age <= 65 THEN '56-65'
        else '65+'
    end
order by supscription_rate_pct desc;