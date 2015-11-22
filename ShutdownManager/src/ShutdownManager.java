import org.bukkit.Bukkit;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.event.player.PlayerKickEvent;
import org.bukkit.plugin.java.JavaPlugin;
import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;

public class ShutdownManager extends JavaPlugin implements Listener {
    private int playerCount;
    private Timer countdown;
    
    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(this, this);
        playerCount = getServer().getOnlinePlayers().size();
        countdown = new Timer();
        
        if (playerCount == 0)
            startCountdown();
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        playerCount++;
        if (playerCount == 1)
            countdown.cancel();
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        playerCount--;
        if (playerCount == 0)
            startCountdown();
    }

    @EventHandler
    public void onPlayerKick(PlayerKickEvent event) {
        playerCount--;
        if (playerCount == 0)
            startCountdown();
    }

    public void startCountdown() {
        countdown = new Timer();
        countdown.schedule(new TimerTask() {
            public void run() {
                getServer().shutdown();
            }
        }, new Date(new Date().getTime() + 900000));
    }
}
