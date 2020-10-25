% tsl_week_8.m
% Written by Joshua Holbrook, week of March 28th 2010
% Since people actually seem to be using this, it's licensed 
% under the WTFPL (http://sam.zoy.org/wtfpl/).

% A little snafu with matlab is that you can't define a function within a
% non-function script. So, I wrapped these codes in a function!
function tsl_week_8()

    % Prompt 1: *Using Matlab*, perform a sum of least squares non-linear 
    % power regression for the speed vs. flow rate, pressure drop, & pump 
    % power.
    %
    % Prompt 2: *Using Matlab, plot the predicted relation over your range
    % of data for the flow vs. speed, pressure vs. speed, & power vs. speed
    % on separate plots.  Include on each of the plots the individual data 
    % points (no regression lines) you collected.
    %
    % This script explains everything I've done in as much detail as I could
    % think to.

    % The following data was inserted via COPY-PASTE WOOO
    % I should find a good way to read values direct from excel.
    % (note: xlsread() may be able to do it.)
    % I could totally do this with python--I wonder how much of a PITA 
    % it would be?
    %
    % ANYWAYS
    %
    % Think of these as tables, not matrices. No trickery going on!

    % rpm values for each of the four runs.
    rpm=[498,498,499,499,500;
         1102,1103,1104,1105,1109;
         1736,1737,1740,1746,1750;
         2505,2509,2512,2524,2532];

    % Corresponding flow rates
    flow=[10.70,8.02,5.28,2.50,0.00;
          24.25,18.28,12.12,6.11,0.00;
          38.38,28.65,19.17,9.54,0.00;
          55.35,41.56,28.00,13.98,0.00];

    % Corresponding pressure drops
    pdrop=[0.2,0.5,0.8,0.8,0.8;
            1.6,3.4,4.3,4.8,5.0;
            4.1,8.9,11.1,12.3,12.6;
            8.6,18.9,23.8,26.1,26.5];

    % Corresponding BHP
    bhp=[0.019,0.019,0.017,0.016,0.014;
         0.127,0.115,0.099,0.084,0.063;
         0.436,0.393,0.332,0.261,0.192;
         1.230,1.099,0.899,0.702,0.494];
     
    % Oh, and we'll want valve settings. You'll see why.
    valve=[1.00,0.75,0.50,0.25,0.00];

    % Now for some curve fitting action!
    function [a,r2] = curvefitaction(xdata,ydata)
        % This is where the magic happens.
        % matlab has a metric butt-ton of optimization functions which may 
        % be used for curve-fitting in one way or another. These include 
        % the really basic fminsearch(), tools from the statistics
        % toolbox, functions from the optimization toolbox (my favorite) 
        % and even a separate curvefit toolbox! Because the optimization 
        % toolbox seems pretty ubiquitous, and the particular function is
        % easy to use (imo), I chose to use lsqcurvefit(). Just throwing 
        % out there that many alternatives exist!
        %
        % This is how you use lsqcurvefit:

        [a,r2] = lsqcurvefit(@(a,x) a(1).*x.^a(2),[1.0,2.0],xdata, ydata);

        % Now for some explanation. This function takes the form:
        %
        %     aout = lsqcurvefit(function(a,x), a0, x,y)
        %
        % a is a vector containing all the values you want to change, a0 is
        % an initial guess ([1.0,1.5] in my case, for a function 
        % y=1.*x.^1.5) and x is a vector of input values. Naturally, y is 
        % the vector of output data that you're matching to.
        %
        % In this particular case, I used what's called an "anonymous 
        % function" so that I don't have to define it elsewhere, but that's
        % not necessary! For example, I could've defined the function like 
        % so:
        %
        %    function y = apow(a,x)
        %        y = a(1).*x.^a(2);
        %    end
        %
        % and then use it with lsqcurvefit like so:
        %
        %     lsqcurvefit(@apow,[1.0,1.5], xdata, ydata)
        %
        % Naturally, your mileage may vary.
        %
        % Another concern is that, when running these, I get the following
        % message:
        %
        % >  Optimization terminated: first-order optimality less than 
        % >  OPTIONS.TolFun, and no negative/zero curvature detected in 
        % >  trust region model.
        %
        % My understanding is that this means "everything looks to be in
        % order, so we're terminating," and as such I'm not too worried.
        % However, if you're concerned and want to explore changing the
        % termination defaults, you can learn about how to do this by
        % typing "help optimset" in the matlab terminal.
        %
        % Note that that this function, in its current form, is a
        % one-liner excepting for comments. Having a function like this 
        % that makes things easy is where matlab really shines! 
        % Unfortunately, writing it yourself can be annoying.
    end

    % A function that normalizes the data to the last value in each row.
    function A = normalize(A)
        % You could easily just do this, y'know, not as a function, but you
        % know how I like to complicate things! One handy reason for doing
        % this is that I can change the baseline for everything without
        % having to change every line where I use normalize().
        %
        % All I do is divide every table by the bottom-left-most value
        % in the table. This means I chose the max RPM at 100% flow as my
        % baseline point (You want to use the same baseline for all values,
        % and you don't want any zero-values).
        
        A=A./A(size(A,1),1);
        
        % In some languages, you could use the index -1 to represent the
        % last value in the array. I like this and I wish I could do that 
        % here! Note, these languages all roll 0-index arrays, 
        % not 1-index matrices.
    end

    % Now, we can get some work done!
    % What are we doing again? Oh, yes:
    % >  Prompt 1: *Using Matlab*, perform a sum of least squares non-linear 
    % >  power regression for the speed vs. flow rate, pressure drop, & pump 
    % >  power.
    %
    % >  Prompt 2: *Using Matlab, plot the predicted relation over your range
    % >  of data for the flow vs. speed, pressure vs. speed, & power vs. speed
    % >  on separate plots.  Include on each of the plots the individual data 
    % >  points (no regression lines) you collected.
       
    % x is a range of (normalized) rpms, used for graphing. You'll see it 
    % come up later. I use the same trick as is in normalize() to divide it
    % by the baseline rpm. This is something you could do separately for
    % each data set, like I mentioned in the normalize() function.
    x=linspace(450,2600,100)./rpm(size(rpm,1),1);

    % Now, we normalize all the data sets, including rpm, since I don't
    % need rpm_0 anymore.
    rpm = normalize(rpm);
    flow = normalize(flow);
    pdrop = normalize(pdrop);
    bhp = normalize(bhp);

    % We'll start with a naive reporting of speed vs. flow rate:
    %
    % I used obnoxious formatting stuff for prettier output.
    % If you don't care about how things look, you can just decide to not
    % surpress function output, and just read a and r2 that way.
    fprintf('\nNaive Flow Rate vs Speed:\n=====================\n')
    [a,r2] = curvefitaction(rpm, flow);
    fprintf('\n(N/N_0) = %-3.2f * (Q/Q_0)^ %-3.2f \n',a(1),a(2));
    fprintf('Residual squared: %-3.2f\n\n',r2);
    
    % We also desire to output a graph.
    % Because of the way I shaped the input data and how matlab expects to
    % receive its y values as a vector (as an array, it plots them as
    % different sets against x), I used matlab's reshape() function
    % to make them 1x20 instead of 4x5. The order's pretty jacked up in my
    % opinion, but as long as the way matlab reorders everything is
    % consistent (it should be) I think it'll be okay.
    
    figure;
    % This line plots the lsqcurvefit-generated curve.
    plot(x, a(1).*x.^a(2),'b-');
    hold on;
    % This line plots the original data points.
    plot(reshape(rpm,1,[]),reshape(flow,1,[]),'kd');
    title('Naive Curve Fit of Flow Rate vs. Speed');
    xlabel('rpm/rpmo');
    ylabel('Q/Qo');
    
    % Look at this figure. You can see that, unfortunately, that there's
    % another variable at work here, and in retrospect it should've been
    % obvious. That variable is valve setting.
    % 
    % There are multiple ways to get around this issue, but I think the
    % easiest is to do separate curve fits for each flow rate:
    
    % Initializing storage for a and r:
    a=zeros(size(valve,2),2);
    r2=zeros(size(valve))';
    
    for i=1:size(valve,2),
        [a(i,:),r2(i)]=curvefitaction(rpm(:,i),flow(:,i));
    end
    
    fprintf('\n\n\nFlow Rate vs Speed:\n=====================\n')    
    fprintf('\n%%flow_a(1)__a(2)__|_r^2_\n');
    for i=1:size(valve,2),
        fprintf('%-5.2f %-5.2f %-5.2f | %-1.2e \n',valve(i),a(i,:),r2(i));
    end
        
    % ...and now that we have that:

    figure;
    
    % Commented here is code that will plot the regression curves, but for 
    % the purposes of the lab it's not useful for anything more than 
    % personal interest. Feel free to un-comment/borrow if you like!
    % Here, I used meshgrid to make the y matrix. meshgrid is very useful 
    % for vectorizing output, if that's how you like to think about these 
    % kinda things. Others prefer to roll for loops, and with today's 
    % java-driven matlab, this is okay!
    % Anyway, if you want to understand this, try meshgrid out in 
    % interactive mode to see what it does!
    %[xgrid,a1grid]=meshgrid(x,a(:,1));
    %[xgrid,a2grid]=meshgrid(x,a(:,2)); % matlab, afaik, forces me to do 
                                       % something with the first output :(
    %plot(x, a1grid.*xgrid.^a2grid,'b-');
    
    % It turns out plotting is way easy, because Bargar doesn't want the
    % regression lines! What he wants is the pump affinity law curves!
    plot(x, x,'b-');
    hold on;
    % This line plots the original data points.
    plot(reshape(rpm,1,[]),reshape(flow,1,[]),'kd');
    title('Flow Rate vs. Speed');
    xlabel('rpm/rpmo');
    ylabel('Q/Qo');
        
    % At this point, we rinse-and-repeat for the rest of the data sets.
    % I could've turned this into a function, but whatever.
    
    % ==Speed v. p-drop==
    for i=1:size(valve,2),
        [a(i,:),r2(i)]=curvefitaction(rpm(:,i),pdrop(:,i));
    end
    
    fprintf('\n\n\nPressure Drop vs Speed:\n=======================\n')    
    fprintf('\n%%flow_a(1)__a(2)__|_r^2_\n');
    for i=1:size(valve,2),
        fprintf('%-5.2f %-5.2f %-5.2f | %-1.2e \n',valve(i),a(i,:),r2(i));
    end
        
    figure;
    %[xgrid,a1grid]=meshgrid(x,a(:,1));
    %[xgrid,a2grid]=meshgrid(x,a(:,2));
    %plot(x, a1grid.*xgrid.^a2grid,'b-');
    plot(x, x.^2.0,'b-');
    hold on;
    plot(reshape(rpm,1,[]),reshape(pdrop,1,[]),'kd');
    title('Pressure Drop vs. Speed');
    xlabel('rpm/rpmo');
    ylabel('dP/dPo');
    
    % ==Speed v. bhp==
    for i=1:size(valve,2),
        [a(i,:),r2(i)]=curvefitaction(rpm(:,i),bhp(:,i));
    end
    
    fprintf('\n\n\nBrake Horsepower vs Speed:\n==========================\n')
    fprintf('\n%%flow_a(1)__a(2)__|_r^2_\n');
    for i=1:size(valve,2),
        fprintf('%-5.2f %-5.2f %-5.2f | %-1.2e \n',valve(i),a(i,:),r2(i));
    end
        
    figure;
    %[xgrid,a1grid]=meshgrid(x,a(:,1));
    %[xgrid,a2grid]=meshgrid(x,a(:,2));
    %plot(x, a1grid.*xgrid.^a2grid,'b-');
    plot(x, x.^3.0,'b-');
    hold on;
    plot(reshape(rpm,1,[]),reshape(bhp,1,[]),'kd');
    title('Brake Horsepower vs. Speed');
    xlabel('rpm/rpmo');
    ylabel('HP/HPo');
    
end