bleh=regexp(BesteVitro.grRules,'(');
blehR=regexp(BesteVitro.grRules,'R');
BesteGR2 = BesteVitro.grRules;

for i = 1:size(bleh)
    if ~isempty(blehR{i})
        if isempty(bleh{i})
            count = 0;
            for j = 1:numel(blehR{i})
                if blehR{i}(j) == 1
                    BesteGR2{i} = ['(' BesteGR2{i}];
                else
                    BesteGR2{i} = [BesteGR2{i}(1:blehR{i}(j)+count-1) '(' BesteGR2{i}(blehR{i}(j)+count:end)];
                end
                count = count+1;
            end
        end
    end
end

bleh2=regexp(BesteGR2,')');
[mstart mend]=regexp(BesteGR2,'\w{2}[0-9]{4}');

for i = 1:size(bleh2)
    if ~isempty(mend{i})
        if isempty(bleh2{i})
            count = 0;
            for j = 1:numel(mend{i})
                c2 = 0;
                if mend{i}(j)+count < numel(BesteGR2{i}) 
                    if isequal(BesteGR2{i}(mend{i}(j)+count+1),'c') | isequal(BesteGR2{i}(mend{i}(j)+count+1),'A')
                        c2 = 1;
                    end
                end
                if mend{i}(j)+count+c2 == numel(BesteGR2{i})
                    BesteGR2{i} = [BesteGR2{i} ')'];
                else
                    BesteGR2{i} = [BesteGR2{i}(1:mend{i}(j)+c2+count) ')' BesteGR2{i}(mend{i}(j)+c2+count+1:end)];
                end
                count = count+1;
            end
        end
    end
end