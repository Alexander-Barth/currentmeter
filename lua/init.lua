dofile("connect.lua")

-- get effective current in mA
function getCurrent()
   local mean = 0
   -- number of samples (tests show that N=125 correspond approx. to 10 50-60 Hz cycle)
   local N = 125
   -- adc.read value when there is no current
   local adc0 = 533
   -- burden resistor (Ohm)
   local Rburden = 22
   -- Reference voltage (mV)
   local Vref = 3300
   -- number of turns in sensor devided by 100
   local CT_turns = 20

   for i=1,N do
      mean = mean + (adc.read(0)-adc0)^2
      -- delay 1000us
      tmr.delay(1000)
   end

   print(mean/N)
   -- multiply by 10000 (100^2) for better precision in sqrt
   mean = (mean*10000)/N

   -- current in mA
   return (math.sqrt(mean) * Vref * CT_turns) / (1024 * Rburden)
end


-- the http server
srv=net.createServer(net.TCP) 
srv:listen(80,function(conn) 
    conn:on("receive",function(conn,payload) 
    print(payload) 

    conn:send(table.concat({
         'HTTP/1.1 200 OK', 
         'Access-Control-Allow-Origin: *',
         'Content-Type: application/json','',''},'\r\n'))
    conn:send(cjson.encode({current=getCurrent()}))    
    end) 
end)
